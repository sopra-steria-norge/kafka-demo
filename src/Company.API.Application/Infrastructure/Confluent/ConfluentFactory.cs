using System.Collections.Concurrent;
using Company.API.Application.Infrastructure.Consumer;
using Company.API.Application.Infrastructure.Producer;
using Confluent.Kafka;
using Confluent.Kafka.SyncOverAsync;
using Confluent.SchemaRegistry;
using Confluent.SchemaRegistry.Serdes;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace Company.API.Application.Infrastructure.Confluent;

public class ConfluentFactory : IProducerFactory, IConsumerFactory, IAdminFactory
{
    private readonly ILogger<ConfluentFactory> _logger;
    private readonly ConfluentOptions _confluentOptions;

    private readonly ConcurrentDictionary<string, object> _producerCache = new();
    private readonly ConcurrentDictionary<string, object> _consumerCache = new();
    private readonly ISchemaRegistryClient _schemaRegistryClient;

    private IAdminClient? _adminClient = null;

    public ConfluentFactory(
        ILogger<ConfluentFactory> logger,
        IOptions<ConfluentOptions> confluentOptions,
        ISchemaRegistryClient schemaRegistryClient
    )
    {
        _logger = logger;
        _confluentOptions = confluentOptions.Value;
        _schemaRegistryClient = schemaRegistryClient;
    }

    public IAdminClient GetAdminClient()
    {
        if (_adminClient is not null)
            return _adminClient;

        var config = new AdminClientConfig { BootstrapServers = _confluentOptions.BrokerUrl };

        _adminClient = new AdminClientBuilder(config).Build();

        return _adminClient;
    }

    public IProducer<TKey, TValue> CreateProtobufProducer<TKey, TValue>(
        string name,
        ProducerConfig config,
        bool serialize = true
    )
        where TValue : class, Google.Protobuf.IMessage<TValue>, new()
    {
        var cachedProducer = CheckProducerCache<TKey, TValue>(name);
        if (cachedProducer != null)
            return cachedProducer;

        config.BootstrapServers = _confluentOptions.BrokerUrl;
        var producerBuilder = new ProducerBuilder<TKey, TValue>(config);

        if (serialize)
            producerBuilder.SetValueSerializer(
                new ProtobufSerializer<TValue>(_schemaRegistryClient)
            );

        var producer = producerBuilder.Build();

        return TryAddToProducerCache(name, producer);
    }

    public IProducer<TKey, TValue> CreateProducer<TKey, TValue>(string name, ProducerConfig config)
    {
        var cachedProducer = CheckProducerCache<TKey, TValue>(name);
        if (cachedProducer != null)
            return cachedProducer;

        config.BootstrapServers = _confluentOptions.BrokerUrl;
        var producer = new ProducerBuilder<TKey, TValue>(config).Build();

        return TryAddToProducerCache(name, producer);
    }

    private IProducer<TKey, TValue> TryAddToProducerCache<TKey, TValue>(
        string name,
        IProducer<TKey, TValue> producer
    )
    {
        try
        {
            if (_producerCache.TryAdd(name, producer))
                return producer;
        }
        catch (ArgumentNullException e)
        {
            _logger.LogError(e, e.Message);
        }
        catch (OverflowException e)
        {
            _logger.LogCritical(e, e.Message);
            throw;
        }

        throw new Exception("Could not add producer to cache");
    }

    private IProducer<TKey, TValue>? CheckProducerCache<TKey, TValue>(string name)
    {
        if (_producerCache.TryGetValue(name, out var cachedProducer))
            return (IProducer<TKey, TValue>)cachedProducer;

        return null;
    }

    public IConsumer<TKey, TValue> CreateProtobufConsumer<TKey, TValue>(
        string name,
        ConsumerConfig config,
        bool serialize = true
    )
        where TValue : class, Google.Protobuf.IMessage<TValue>, new()
    {
        var cachedConsumer = CheckConsumerCache<TKey, TValue>(name);
        if (cachedConsumer != null)
            return cachedConsumer;

        config.BootstrapServers = _confluentOptions.BrokerUrl;
        var consumerBuilder = new ConsumerBuilder<TKey, TValue>(config);

        if (serialize)
            consumerBuilder.SetValueDeserializer(
                new ProtobufDeserializer<TValue>().AsSyncOverAsync()
            );

        var consumer = consumerBuilder.Build();

        return TryAddToConsumerCache(name, consumer);
    }

    public IConsumer<TKey, TValue> CreateConsumer<TKey, TValue>(string name, ConsumerConfig config)
    {
        var cachedConsumer = CheckConsumerCache<TKey, TValue>(name);
        if (cachedConsumer != null)
            return cachedConsumer;

        config.BootstrapServers = _confluentOptions.BrokerUrl;
        var consumer = new ConsumerBuilder<TKey, TValue>(config).Build();

        return TryAddToConsumerCache(name, consumer);
    }

    private IConsumer<TKey, TValue> TryAddToConsumerCache<TKey, TValue>(
        string name,
        IConsumer<TKey, TValue> consumer
    )
    {
        try
        {
            if (_consumerCache.TryAdd(name, consumer))
                return consumer;
        }
        catch (ArgumentNullException e)
        {
            _logger.LogError(e, e.Message);
        }
        catch (OverflowException e)
        {
            _logger.LogCritical(e, e.Message);
            throw;
        }

        throw new Exception("Could not add producer to cache");
    }

    private IConsumer<TKey, TValue>? CheckConsumerCache<TKey, TValue>(string name)
    {
        if (_consumerCache.TryGetValue(name, out var consumer))
            return (IConsumer<TKey, TValue>)consumer;

        return null;
    }

    public void CleanUpConsumer<TKey, TValue>(string name)
    {
        var cachedConsumer = CheckConsumerCache<TKey, TValue>(name);
        if (cachedConsumer != null)
        {
            cachedConsumer.Close();
            _consumerCache.TryRemove(name, out _);
        }
    }

    public void Dispose()
    {
        _adminClient?.Dispose();
    }
}
