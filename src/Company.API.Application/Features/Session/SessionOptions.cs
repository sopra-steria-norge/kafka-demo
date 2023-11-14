using FluentValidation;

namespace Company.API.Application.Features.Session;

public sealed record SessionOptions
{
    public const string SectionName = "Session";

    public int SessionMinimumYear { get; init; } = 1950;

    public int SessionMaximumYear { get; init; } = DateTime.UtcNow.Year;
}

public class SessionOptionValidation : AbstractValidator<SessionOptions>
{
    public SessionOptionValidation()
    {
        RuleFor(option => option.SessionMaximumYear).NotNull().NotEmpty();

        RuleFor(option => option.SessionMinimumYear).NotNull().NotEmpty();
    }
}
