using System.Text;
using Microsoft.Extensions.DependencyInjection;
using Company.API.Application.Features.Session;
using Company.API.Application.Infrastructure.Consumer;
using Confluent.Kafka;
using Company.Proto.Formula1.Request;
using FluentAssertions;

namespace Company.API.IntegrationTests.Features.SessionAndLongRunningOperations;

public static class SessionHelpers
{
    public static void SessionRequestTestHelper(
        this IServiceScope scope,
        SessionRequest request,
        SessionResponse? response
    )
    {
        var consumerFactory = scope.ServiceProvider.GetRequiredService<IConsumerFactory>();

        var consumerConfig = new ConsumerConfig()
        {
            GroupId = "test.request",
            AutoOffsetReset = AutoOffsetReset.Earliest,
            EnableAutoOffsetStore = false,
            EnablePartitionEof = true
        };

        var requestConsumer = consumerFactory.CreateProtobufConsumer<Null, RequestSession>(
            "test",
            consumerConfig
        );
        requestConsumer.Subscribe("f1.session-request.event.proto.v1");

        while (true)
        {
            var cancelationTokenSource = new CancellationTokenSource();
            cancelationTokenSource.CancelAfter(TimeSpan.FromMilliseconds(2000));

            var consumerResult = requestConsumer.Consume(cancelationTokenSource.Token);
            if (consumerResult.Message.Value is not null)
            {
                var data = consumerResult.Message.Value;
                var headers = consumerResult.Message.Headers.BackingList;

                var correlationId = headers.First(x => x.Key == "ce_correlationid");
                var correlationIdString = Encoding.UTF8.GetString(correlationId.GetValueBytes());

                correlationIdString.Should().Be(response?.OperationId.ToString());

                data.CarData.Should().BeFalse();
                data.PositionData.Should().BeTrue();
                data.Identifier.Should().Be(Identifiers.Race);
                data.GrandPrix.Should().Be(5);
                data.Year.Should().Be(2023);

                break;
            }
        }
    }
}
