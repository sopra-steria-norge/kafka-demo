using FluentValidation;
using FluentValidation.Results;

using MediatR;

namespace Company.API.Application.Validation;

public sealed class ValidationBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : notnull
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken
    )
    {
        var context = new ValidationContext<TRequest>(request);

        var validationFailures = await Task.WhenAll(
            _validators.Select(validators => validators.ValidateAsync(context, cancellationToken))
        );

        var errors = validationFailures
            .Where(result => !result.IsValid)
            .SelectMany(result => result.Errors)
            .Select(failure => new ValidationFailure(failure.PropertyName, failure.ErrorMessage))
            .ToList();

        if (errors.Any())
            throw new ValidationException(errors);

        var response = await next();

        return response;
    }
}
