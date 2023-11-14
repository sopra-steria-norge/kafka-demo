using FluentAssertions;

namespace Company.API.Application.UnitTests;

public class TestConfluentClusterOptions
{
    [Fact]
    public void Confluent_Cluster_Options_Should_Be_Success()
    {
        // Setup
        var options = new ConfluentOptions { BrokerUrl = "localhost:9092" };
        var validator = new ConfluentClusterOptionValidation();

        // Act
        var result = validator.Validate(options);

        // Assert
        result.IsValid.Should().BeTrue();
    }

    [Fact]
    public void Confluent_Cluster_Options_Should_Be_Failure()
    {
        // Setup
        var options = new ConfluentOptions();
        var validator = new ConfluentClusterOptionValidation();

        // Act
        var result = validator.Validate(options);

        // Assert
        result.IsValid.Should().BeFalse();
        result.Errors.Should().NotBeEmpty();
    }
}
