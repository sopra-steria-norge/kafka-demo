using FluentValidation;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;

namespace Company.API.Application.Validation;

/// <summary>
/// Extension methods for OptionBuilder to add validation by using Fluentvalidation.
/// </summary>
public static class OptionBuilderFluentValidationExtensions
{
    public static OptionsBuilder<TOptions> ValidateFluently<TOptions>(
        this OptionsBuilder<TOptions> optionsBuilder
    )
        where TOptions : class
    {
        optionsBuilder.Services.AddSingleton<IValidateOptions<TOptions>>(
            s =>
                new FluentValidationOptions<TOptions>(
                    optionsBuilder.Name,
                    s.GetRequiredService<IValidator<TOptions>>()
                )
        );
        return optionsBuilder;
    }
}

/// <summary>
///
/// </summary>
/// <typeparam name="TOptions"></typeparam>
public class FluentValidationOptions<TOptions> : IValidateOptions<TOptions>
    where TOptions : class
{
    private readonly IValidator<TOptions> _validator;

    public FluentValidationOptions(string? name, IValidator<TOptions> validator)
    {
        Name = name;
        _validator = validator;
    }

    public string? Name { get; }

    public ValidateOptionsResult Validate(string? name, TOptions options)
    {
        if (Name != null && Name != name)
            return ValidateOptionsResult.Skip;

        ArgumentNullException.ThrowIfNull(options);

        var validationResult = _validator.Validate(options);

        if (validationResult.IsValid)
            return ValidateOptionsResult.Success;

        var errors = validationResult.Errors.Select(
            x => $"Options validation failed for {x.PropertyName} with error: {x.ErrorMessage}"
        );

        return ValidateOptionsResult.Fail(errors);
    }
}
