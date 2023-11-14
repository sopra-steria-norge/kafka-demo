using Confluent.Kafka;
using Google.Protobuf;

namespace Company.API.Application.Infrastructure.Consumer;

public interface IConsumerFactory
{
    void CleanUpConsumer<TKey, TValue>(string name);

    IConsumer<TKey, TValue> CreateConsumer<TKey, TValue>(string name, ConsumerConfig config);

    IConsumer<TKey, TValue> CreateProtobufConsumer<TKey, TValue>(
        string name,
        ConsumerConfig config,
        bool serialize = true
    )
        where TValue : class, IMessage<TValue>, new();
}
