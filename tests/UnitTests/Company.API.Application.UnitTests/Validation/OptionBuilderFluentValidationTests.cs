using FluentAssertions;
using FluentValidation;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;

using Company.API.Application.Validation;

namespace Company.API.Application.UnitTests.Validation;

public record TestOption
{
    public const string SectionName = "Test";

    public string Name { get; set; } = string.Empty;

    public int Number { get; set; } = 0;
}

public class TestOptionsValidation : AbstractValidator<TestOption>
{
    public TestOptionsValidation()
    {
        RuleFor(x => x.Name).NotEmpty().NotNull();

        RuleFor(x => x.Number).LessThan(1);
    }
}

public class OptionValidation
{
    [Fact]
    public void Options_Should_Be_Test()
    {
        // Setup
        IServiceCollection services = new ServiceCollection();

        services.AddTransient<IValidator<TestOption>, TestOptionsValidation>();
        services.AddOptions<TestOption>().Configure(o => o.Name = "Test").ValidateFluently();

        var provider = services.BuildServiceProvider();

        // Act
        var options = provider.GetRequiredService<IOptions<TestOption>>().Value;

        // Assert
        options.Name.Should().Be("Test");
    }

    [Fact]
    public void Option_Validation_Should_Be_Skipped()
    {
        // Setup
        var validator = new TestOptionsValidation();
        var optionValidator = new FluentValidationOptions<TestOption>("Data", validator);

        var option = new TestOption { Name = "Test" };

        // Act
        var result = optionValidator.Validate("Test", option);

        // Assert
        result.Should().Be(ValidateOptionsResult.Skip);
    }

    [Fact]
    public void Option_Validation_Should_Be_Skipped_When_Name_Is_Not_Equal()
    {
        // Setup
        var validator = new TestOptionsValidation();
        var optionValidator = new FluentValidationOptions<TestOption>("Data", validator);

        var option = new TestOption { Name = "Test" };

        // Act
        var result = optionValidator.Validate("Test", option);

        // Assert
        result.Should().Be(ValidateOptionsResult.Skip);
    }

    [Fact]
    public void Option_Validation_Should_Be_Skipped_When_Name_Is_Null()
    {
        // Setup
        var validator = new TestOptionsValidation();
        var optionValidator = new FluentValidationOptions<TestOption>(null, validator);

        var option = new TestOption { Name = "Test" };

        // Act
        var result = optionValidator.Validate("", option);

        // Assert
        result.Should().Be(ValidateOptionsResult.Success);
    }

    [Fact]
    public void Option_Validation_Option_Null_Should_Throw_ArgumentNullException()
    {
        // Setup
        var validator = new TestOptionsValidation();
        var optionValidator = new FluentValidationOptions<TestOption>("", validator);

        // Act / Assert
        optionValidator
            .Invoking(o => o.Validate("", null!))
            .Should()
            .Throw<ArgumentNullException>()
            .WithMessage("Value cannot be null. (Parameter 'options')");
    }

    [Fact]
    public void Option_Validation_Should_Fail()
    {
        // Setup
        IServiceCollection services = new ServiceCollection();

        services.AddTransient<IValidator<TestOption>, TestOptionsValidation>();
        services
            .AddOptions<TestOption>()
            .Configure(o =>
            {
                o.Name = "Test";
                o.Number = 5;
            })
            .ValidateFluently();

        var provider = services.BuildServiceProvider();

        // Act / Assert
        provider
            .Invoking(x => x.GetRequiredService<IOptions<TestOption>>().Value)
            .Should()
            .Throw<OptionsValidationException>()
            .WithMessage(
                "Options validation failed for Number with error: 'Number' must be less than '1'."
            );
    }
}
