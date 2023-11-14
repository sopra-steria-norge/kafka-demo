using System.Text;
using Confluent.Kafka;
using Confluent.Kafka.Admin;
using DotNet.Testcontainers.Builders;
using DotNet.Testcontainers.Configurations;
using DotNet.Testcontainers.Containers;

namespace Company.API.IntegrationTests;

/// <summary>
/// This is testcontainer fixture for starting an kafka with an schema registry container.
/// </summary>
public class KafkaFixture
{
    private IContainer? _kafkaContainer;

    private IContainer? _srContainer;

    private const string StartupScriptFilePath = "/testcontainers.sh";

    public const int SchemaRegistryPort = 8081;

    public const int KafkaPort = 9092;

    public const int BrokerPort = 9093;

    public const int BrokerUi = 29094;

    public const int ZookeeperPort = 2181;

    /// <summary>
    /// Set the image and tag to be used to create Kafka
    /// </summary>
    public string KafkaImage { get; set; } = "confluentinc/cp-kafka:7.5.0";

    /// <summary>
    /// Set the image and tag to be used to create schema registry
    /// </summary>
    public string SchemaRegistryImage { get; set; } = "confluentinc/cp-schema-registry:7.5.0";

    /// <summary>
    /// The bootstrap server to be used during testing scenarios
    /// </summary>
    public string BootstrapServers
    {
        get
        {
            return $"{_kafkaContainer!.Hostname}:{_kafkaContainer.GetMappedPublicPort(KafkaPort)}";
        }
    }

    /// <summary>
    /// Shutdown the containers
    /// </summary>
    /// <returns></returns>
    public async Task DisposeAsync()
    {
        await _kafkaContainer!.StopAsync();
        await _srContainer!.StopAsync();
    }

    /// <summary>
    /// Start Kafka container and link the schema registry with the kafka container.
    /// </summary>
    /// <returns></returns>
    public async Task InitializeAsync()
    {
        await CreateKafka();
        await CreateSchemaRegistry();
    }

    private async Task CreateKafka()
    {
        _kafkaContainer = new ContainerBuilder()
            .WithName("producer-kafka")
            .WithImage(KafkaImage)
            .WithPortBinding(KafkaPort, true)
            .WithPortBinding(BrokerPort, true)
            .WithPortBinding(ZookeeperPort, true)
            .WithPortBinding(BrokerUi, true)
            .WithEnvironment(
                "KAFKA_LISTENERS",
                "PLAINTEXT://0.0.0.0:"
                    + KafkaPort
                    + ",BROKER://0.0.0.0:"
                    + BrokerPort
                    + ",UI://0.0.0.0:"
                    + BrokerUi
            )
            .WithEnvironment(
                "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP",
                "BROKER:PLAINTEXT,PLAINTEXT:PLAINTEXT,UI:PLAINTEXT"
            )
            .WithEnvironment("KAFKA_INTER_BROKER_LISTENER_NAME", "BROKER")
            .WithEnvironment("KAFKA_BROKER_ID", "1")
            .WithEnvironment("KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR", "1")
            .WithEnvironment("KAFKA_OFFSETS_TOPIC_NUM_PARTITIONS", "1")
            .WithEnvironment("KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR", "1")
            .WithEnvironment("KAFKA_TRANSACTION_STATE_LOG_MIN_ISR", "1")
            .WithEnvironment("KAFKA_LOG_FLUSH_INTERVAL_MESSAGES", long.MaxValue.ToString())
            .WithEnvironment("KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS", "0")
            .WithEnvironment("KAFKA_ZOOKEEPER_CONNECT", "localhost:" + ZookeeperPort)
            .WithEnvironment("KAFKA_SCHEMA_REGISTRY_URL", $"schema-registry:{SchemaRegistryPort}")
            .WithEntrypoint("/bin/sh", "-c")
            .WithCommand(
                "while [ ! -f "
                    + StartupScriptFilePath
                    + " ]; do sleep 0.1; done; "
                    + StartupScriptFilePath
            )
            .WithWaitStrategy(
                Wait.ForUnixContainer().UntilMessageIsLogged("\\[KafkaServer id=\\d+\\] started")
            )
            .WithStartupCallback(
                (container, ct) =>
                {
                    const char lf = '\n';
                    var startupScript = new StringBuilder();
                    startupScript.Append("#!/bin/bash");
                    startupScript.Append(lf);
                    startupScript.Append(
                        "echo 'clientPort=" + ZookeeperPort + "' > zookeeper.properties"
                    );
                    startupScript.Append(lf);
                    startupScript.Append(
                        "echo 'dataDir=/var/lib/zookeeper/data' >> zookeeper.properties"
                    );
                    startupScript.Append(lf);
                    startupScript.Append(
                        "echo 'dataLogDir=/var/lib/zookeeper/log' >> zookeeper.properties"
                    );
                    startupScript.Append(lf);
                    startupScript.Append("zookeeper-server-start zookeeper.properties &");
                    startupScript.Append(lf);
                    startupScript.Append(
                        "export KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://"
                            + container.Hostname
                            + ":"
                            + container.GetMappedPublicPort(KafkaPort)
                            + ",BROKER://"
                            + container.IpAddress
                            + ":"
                            + BrokerPort
                            + ",UI://"
                            + container.IpAddress
                            + ":"
                            + BrokerUi
                    );
                    startupScript.Append(lf);
                    startupScript.Append("echo '' > /etc/confluent/docker/ensure");
                    startupScript.Append(lf);
                    startupScript.Append("/etc/confluent/docker/run");
                    return container.CopyAsync(
                        Encoding.Default.GetBytes(startupScript.ToString()),
                        StartupScriptFilePath,
                        Unix.FileMode755,
                        ct
                    );
                }
            )
            .Build();

        await _kafkaContainer.StartAsync().ConfigureAwait(false);

        await Task.Delay(5000);

        Wait.ForUnixContainer().UntilContainerIsHealthy().UntilPortIsAvailable(KafkaPort);
    }

    private async Task CreateSchemaRegistry()
    {
        _srContainer = new ContainerBuilder()
            .WithName("producer-schema-registry")
            .WithHostname("schema-registry")
            .WithImage(SchemaRegistryImage)
            .WithPortBinding(SchemaRegistryPort, true)
            .WithEnvironment(
                "SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS",
                $"PLAINTEXT://{_kafkaContainer!.IpAddress}:{BrokerPort}"
            )
            .WithEnvironment("SCHEMA_REGISTRY_HOST_NAME", "schema-registry")
            .WithEnvironment("SCHEMA_REGISTRY_LISTENERS", "http://0.0.0.0:" + SchemaRegistryPort)
            .Build();

        await _srContainer.StartAsync().ConfigureAwait(false);

        await Task.Delay(15000);

        Wait.ForUnixContainer().UntilContainerIsHealthy().UntilPortIsAvailable(SchemaRegistryPort);
    }

    public string GetSchemaRegistryUrl()
    {
        var port = _srContainer?.GetMappedPublicPort(SchemaRegistryPort)!;
        return new UriBuilder("http", _srContainer!.Hostname, (int)port).ToString();
    }

    public string GetKafkaBootstrapUrl()
    {
        var port = _kafkaContainer?.GetMappedPublicPort(KafkaPort)!;
        return new UriBuilder("PLAINTEXT", _kafkaContainer!.Hostname, (int)port).ToString();
    }

    /// <summary>
    /// Used to apply an topic to the kafka instance with the given name.
    /// </summary>
    /// <param name="topicName">The name of the kafka topic</param>
    /// <returns></returns>
    public async Task CreateKafkaTopic(string topicName)
    {
        var bootstrapServers = BootstrapServers;

        using var adminClient = new AdminClientBuilder(
            new AdminClientConfig { BootstrapServers = bootstrapServers }
        ).Build();

        await adminClient.CreateTopicsAsync(
            new TopicSpecification[]
            {
                new()
                {
                    Name = topicName,
                    ReplicationFactor = 1,
                    NumPartitions = 1
                }
            }
        );
    }
}
