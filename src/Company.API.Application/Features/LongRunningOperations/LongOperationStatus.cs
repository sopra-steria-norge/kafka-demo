using System.Text.Json.Serialization;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Caching.Memory;
using MediatR;
using ErrorOr;
using FluentValidation;
using Confluent.Kafka;
using Company.Proto.Formula1.Request;
using Company.API.Application.Infrastructure.Consumer;

namespace Company.API.Application.Features.LongRunningOperations;

public sealed record LongOperationResponse
{
    // ReSharper disable once ConvertToPrimaryConstructor
    public LongOperationResponse(DateTime time, Status status)
    {
        Time = time;
        Status = status;
    }

    public DateTime Time { get; init; }

    [JsonConverter(typeof(JsonStringEnumConverter))]
    public Status Status { get; init; }
}

/// <summary>
/// Retrive the satus of an long running opperation.
/// </summary>
public sealed class LongOperationRequest : IRequest<ErrorOr<LongOperationResponse>>
{
    public Guid OperationId { get; init; }
}

public sealed class LongOperationRequestValidator : AbstractValidator<LongOperationRequest>
{
    public LongOperationRequestValidator()
    {
        RuleFor(request => request.OperationId)
            .NotNull()
            .NotEmpty()
            .WithMessage("The 'OperationId' can't be null");

        RuleFor(request => request.OperationId).Must(ValidateGuid).WithErrorCode("Not a Guid");
    }

    private bool ValidateGuid(Guid guid)
    {
        return Guid.TryParse(guid.ToString(), out _);
    }
}

/// <summary>
/// Handles the LongRunningOperationStatus request.
/// </summary>
public sealed class LongRunningOperationHandler
    : IRequestHandler<LongOperationRequest, ErrorOr<LongOperationResponse>>
{
    private readonly ILogger<LongRunningOperationHandler> _logger;
    private readonly IConsumerFactory _consumerFactory;
    private readonly IMemoryCache _cache;

    public LongRunningOperationHandler(
        ILogger<LongRunningOperationHandler> logger,
        IConsumerFactory consumerFactory,
        IMemoryCache cache
    )
    {
        _logger = logger;
        _consumerFactory = consumerFactory;
        _cache = cache;
    }

    /// <summary>
    /// </summary>
    public async Task<ErrorOr<LongOperationResponse>> Handle(
        LongOperationRequest request,
        CancellationToken cancellationToken
    )
    {
        if (_cache.TryGetValue(request.OperationId, out var cacheResult))
        {
            if (cacheResult is not null)
                return (LongOperationResponse)cacheResult!;
        }

        // We need to await something ore else we cant use async, and ErrorOr can be returned as Task.FromResult?
        await Task.Delay(1, cancellationToken);
        var groupId = $"api.session-status.{Guid.NewGuid()}";
        var consumerConfig = new ConsumerConfig
        {
            GroupId = groupId,
            AutoOffsetReset = AutoOffsetReset.Earliest,
            EnableAutoOffsetStore = false,
            EnablePartitionEof = true
        };

        var consumer = _consumerFactory.CreateProtobufConsumer<string, SessionStatusResponse>(
            groupId,
            consumerConfig
        );
        consumer.Subscribe("f1.session-request-status.event.proto.v1");

        LongOperationResponse? response = null;
        try
        {
            var cacheOption = new MemoryCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMilliseconds(10000)
            };

            while (true)
            {
                try
                {
                    var innerCancelationTokenSource = new CancellationTokenSource();

                    using var linkedTokenSource = CancellationTokenSource.CreateLinkedTokenSource(
                        innerCancelationTokenSource.Token,
                        cancellationToken
                    );
                    innerCancelationTokenSource.CancelAfter(TimeSpan.FromMilliseconds(2000));

                    var consumerResult = consumer.Consume(linkedTokenSource.Token);
                    if (consumerResult.Message?.Key == request.OperationId.ToString())
                    {
                        var data = consumerResult.Message.Value;

                        if (data.Status == Status.Completed)
                        {
                            cacheOption = new MemoryCacheEntryOptions
                            {
                                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
                            };
                        }

                        response = new LongOperationResponse(data.Time.ToDateTime(), data.Status);
                        _cache.Set(request.OperationId, response, cacheOption);
                    }
                }
                catch (OperationCanceledException)
                {
                    break;
                }
            }
        }
        catch (ConsumeException e)
        {
            if (e.Error.IsFatal)
            {
                _logger.LogCritical(
                    "Recived Fatal Error: {Code}, {Reason}",
                    e.Error.Code,
                    e.Error.Reason
                );
                throw e;
            }
            _logger.LogError("Recived Error: {Code}, {Reason}", e.Error.Code, e.Error.Reason);
        }

        if (response is null)
            return ErrorOr.Error.NotFound("Operation.NotFound", "We could not find any operation");

        _consumerFactory.CleanUpConsumer<string, SessionStatusResponse>(groupId);
        return response;
    }
}
