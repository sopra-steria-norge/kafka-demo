using Confluent.Kafka;
using Google.Protobuf;

namespace Company.API.Application.Infrastructure.Producer;

public interface IProducerFactory
{
    IProducer<TKey, TValue> CreateProducer<TKey, TValue>(string name, ProducerConfig config);

    IProducer<TKey, TValue> CreateProtobufProducer<TKey, TValue>(
        string name,
        ProducerConfig config,
        bool serialize = true
    )
        where TValue : class, IMessage<TValue>, new();
}
