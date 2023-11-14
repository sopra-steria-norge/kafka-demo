using System.Net.Http.Json;
using Company.API.Application.Features.LongRunningOperations;
using Company.API.Application.Features.Session;
using Company.Proto.Formula1.Request;
using FluentAssertions;
using Microsoft.Extensions.DependencyInjection;

namespace Company.API.IntegrationTests.Features.SessionAndLongRunningOperations;

public class SessionRequestTest
    : IAsyncLifetime,
        IClassFixture<KafkaFixture>,
        IClassFixture<TestWebApplicationFactory<Program>>
{
    private readonly KafkaFixture _kafka;
    private readonly TestWebApplicationFactory<Program> _factory;

    public SessionRequestTest(KafkaFixture kafka, TestWebApplicationFactory<Program> factory)
    {
        _kafka = kafka;
        _factory = factory;
    }

    public async Task InitializeAsync()
    {
        await _kafka.InitializeAsync();
        await _kafka.CreateKafkaTopic("test");

        Environment.SetEnvironmentVariable(
            "ConfluentCluster__BrokerUrl",
            _kafka.GetKafkaBootstrapUrl()
        );
        Environment.SetEnvironmentVariable(
            "ConfluentCluster__SchemaRegistryUrl",
            _kafka.GetSchemaRegistryUrl()
        );
    }

    public async Task DisposeAsync()
    {
        await _kafka.DisposeAsync();
    }

    [Fact]
    public async void WhenRecivingRequest_RequestEventPublished_And_LongOperationStatusSendt_True()
    {
        // Setup
        var client = _factory.CreateClient();
        using var scope = _factory.Services.CreateScope();

        var request = new SessionRequest()
        {
            Year = 2023,
            GrandPrix = 5,
            Identifier = Identifiers.Race,
            CarData = false,
            PositionData = true
        };

        // Act
        var requestResponse = await client.PostAsJsonAsync(new Uri("/sessions/"), request);
        var jsonRequestResponse =
            await requestResponse.Content.ReadFromJsonAsync<SessionResponse>();

        var statusResponse = await client.GetAsync(
            new Uri($"/long-operations/{jsonRequestResponse?.OperationId.ToString()}")
        );
        var jsonOperationResponse =
            await statusResponse.Content.ReadFromJsonAsync<LongOperationResponse>();

        // Assert
        requestResponse.EnsureSuccessStatusCode();

        jsonOperationResponse?.Status.Should().Be(Status.Sendt);
        jsonOperationResponse?.Time.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(10));

        scope.SessionRequestTestHelper(request, jsonRequestResponse);
    }
}
