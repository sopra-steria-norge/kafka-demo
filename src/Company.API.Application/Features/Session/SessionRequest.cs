using System.Text.Json.Serialization;
using Company.API.Application.Infrastructure.Producer;
using Company.API.Application.CloudEvents;
using Company.Proto.Formula1.Request;
using GP = Google.Protobuf.WellKnownTypes;
using Microsoft.Extensions.Logging;
using MediatR;
using ErrorOr;
using FluentValidation;
using Microsoft.Extensions.Options;
using Confluent.Kafka;
using CloudNative.CloudEvents;

using Company.API.Application.Infrastructure;

namespace Company.API.Application.Features.Session;

/// <summary>
/// Response for an session request, with the Long Operation ID.
/// </summary>
public record SessionResponse(Guid OperationId);

/// <summary>
/// The request for an F1 session
/// </summary>
public sealed class SessionRequest : IRequest<ErrorOr<SessionResponse>>
{
    public int Year { get; init; }

    public int GrandPrix { get; init; }

    [JsonConverter(typeof(JsonStringEnumConverter))]
    public Identifiers Identifier { get; init; }

    public bool PositionData { get; init; } = false;

    public bool CarData { get; init; } = false;
}

/// <summary>
/// Validator for an session request.
/// </summary>
public sealed class SessionRequestValidator : AbstractValidator<SessionRequest>
{
    public SessionRequestValidator(IOptions<SessionOptions> options)
    {
        RuleFor(request => request.Year).NotNull().WithMessage("The 'Year' can't be empty");

        RuleFor(request => request.Year)
            .GreaterThanOrEqualTo(options.Value.SessionMinimumYear)
            .LessThanOrEqualTo(options.Value.SessionMaximumYear)
            .WithMessage(
                $"The 'Year' must be between '{options.Value.SessionMinimumYear}' and '{options.Value.SessionMaximumYear}'"
            );

        RuleFor(request => request.GrandPrix)
            .NotNull()
            .WithMessage("The 'GrandPrix' can't be empty");

        RuleFor(request => request.GrandPrix)
            .GreaterThanOrEqualTo(1)
            .LessThanOrEqualTo(20)
            .WithMessage("The 'GrandPrix' must be between '1' and '20''");

        RuleFor(request => request.Identifier)
            .NotNull()
            .WithMessage("The 'Identifier' can't be empty");

        RuleFor(request => request.Identifier)
            .IsInEnum()
            .WithMessage("Identifier must be as specified in enumeration");

        RuleFor(request => request.PositionData)
            .NotNull()
            .WithMessage("'PositionData' can't be null");

        RuleFor(request => request.CarData).NotNull().WithMessage("'PositionData' can't be null");
    }
}

/// <summary>
/// Handle a new session request from an end user. This will craete a new session status then
/// send the request for a F1 session.
/// </summary>
public sealed class SessionHandler : IRequestHandler<SessionRequest, ErrorOr<SessionResponse>>
{
    private readonly ILogger<SessionHandler> _logger;
    private readonly IProducerFactory _producerFactory;
    private readonly IMemoryOperationStorage _operationStorage;

    public SessionHandler(
        ILogger<SessionHandler> logger,
        IProducerFactory producerFactory,
        IMemoryOperationStorage operationStorage
    )
    {
        _logger = logger;
        _producerFactory = producerFactory;
        _operationStorage = operationStorage;
    }

    public async Task<ErrorOr<SessionResponse>> Handle(
        SessionRequest request,
        CancellationToken cancellationToken
    )
    {
        var correlationId = Guid.NewGuid();

        await ProduceStatus(correlationId, cancellationToken);
        await ProduceRequest(request, correlationId, cancellationToken);

        _operationStorage.AddOperationId(correlationId.ToString());

        return new SessionResponse(correlationId);
    }

    /// <summary>
    /// Produce a new session request
    /// </summary>
    private async Task<bool> ProduceRequest(
        SessionRequest request,
        Guid correlationId,
        CancellationToken cancellationToken
    )
    {
        var req = new RequestSession
        {
            Year = request.Year,
            GrandPrix = request.GrandPrix,
            Identifier = (Identifiers)request.Identifier,
            PositionData = request.PositionData,
            CarData = request.CarData
        };

        var cloudEvent = new CloudEvent
        {
            Id = Guid.NewGuid().ToString(),
            Source = new Uri("urn:company:f1:api"),
            Type = "f1.session-request",
            DataContentType = "application/protobuf",
            Subject = "session-request",
            Time = DateTimeOffset.UtcNow
        };

        cloudEvent.SetCorrelationId(correlationId);

        var message = new Message<Null, RequestSession>()
        {
            Value = req,
            Headers = cloudEvent.MapHeaders()
        };

        var config = new ProducerConfig();
        var requestProducer = _producerFactory.CreateProtobufProducer<Null, RequestSession>(
            "request-session",
            config
        );

        _logger.LogDebug("Producing request for F1 session with {Id}", "");
        var result = await requestProducer
            .ProduceAsync("f1.session-request.event.proto.v1", message, cancellationToken)
            .ConfigureAwait(false);

        return true;
    }

    /// <summary>
    /// Produce status for the new request
    /// </summary>
    private async Task<bool> ProduceStatus(Guid correlationId, CancellationToken cancellationToken)
    {
        var sessionStatusResponse = new SessionStatusResponse
        {
            Time = GP.Timestamp.FromDateTime(DateTime.UtcNow),
            Status = Status.Sendt
        };

        var cloudEvent = new CloudEvent
        {
            Id = Guid.NewGuid().ToString(),
            Source = new Uri("urn:company:f1:api"),
            Type = "f1.session-request-status",
            DataContentType = "application/protobuf",
            Subject = "session-request-status",
            Time = DateTimeOffset.UtcNow
        };

        cloudEvent.SetCorrelationId(correlationId);

        var message = new Message<string, SessionStatusResponse>()
        {
            Key = correlationId.ToString(),
            Value = sessionStatusResponse,
            Headers = cloudEvent.MapHeaders()
        };

        var config = new ProducerConfig();
        var producer = _producerFactory.CreateProtobufProducer<string, SessionStatusResponse>(
            "session-status",
            config
        );
        var result = await producer
            .ProduceAsync("f1.session-request-status.event.proto.v1", message, cancellationToken)
            .ConfigureAwait(false);

        return true;
    }
}
