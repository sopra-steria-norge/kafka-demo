using Company.API.Application.Infrastructure;
using Company.API.Application.Infrastructure.Consumer;
using Company.Proto.Formula1.Request;

using Confluent.Kafka;

using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace Company.API.Application.Features.LongRunningOperations;

public class BackgroundStatusWorker : BackgroundService
{
    private readonly ILogger<BackgroundStatusWorker> _logger;
    private readonly IConsumerFactory _consumerFactory;
    private readonly IMemoryCache _cache;
    private readonly IMemoryOperationStorage _operationStorage;

    public BackgroundStatusWorker(
        ILogger<BackgroundStatusWorker> logger,
        IConsumerFactory consumerFactory,
        IMemoryCache cache,
        IMemoryOperationStorage operationStorage
    )
    {
        _logger = logger;
        _consumerFactory = consumerFactory;
        _cache = cache;
        _operationStorage = operationStorage;
    }

    protected override Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Staring up Status Consumer");
        Task.Factory.StartNew(async () => await StatusConsumer(stoppingToken), stoppingToken);

        return Task.CompletedTask;
    }

    private Task StatusConsumer(CancellationToken cancellationToken)
    {
        var groupId = $"api.session-status.{Guid.NewGuid()}";

        var consumerConfig = new ConsumerConfig()
        {
            GroupId = groupId,
            AutoOffsetReset = AutoOffsetReset.Earliest,
            EnableAutoOffsetStore = true,
        };

        var consumer = _consumerFactory.CreateProtobufConsumer<string, SessionStatusResponse>(
            groupId,
            consumerConfig
        );
        consumer.Subscribe("f1.session-request-status.event.proto.v1");

        try
        {
            var cacheOption = new MemoryCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(15)
            };

            while (true)
            {
                try
                {
                    var consumerResult = consumer.Consume(cancellationToken);
                    var data = consumerResult.Message.Value;
                    var key = consumerResult.Message.Key;

                    if (data is null)
                        continue;

                    var response = new LongOperationResponse(data.Time.ToDateTime(), data.Status);
                    _cache.Set(key, response, cacheOption);
                    _operationStorage.AddOperationId(key);
                    _logger.LogInformation("Set cache for {Id}", key);
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

        _consumerFactory.CleanUpConsumer<string, SessionStatusResponse>(groupId);
        return Task.CompletedTask;
    }
}
