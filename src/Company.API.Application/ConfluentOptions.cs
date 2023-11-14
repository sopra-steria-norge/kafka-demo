using FluentValidation;

namespace Company.API.Application;

public class ConfluentOptions
{
    public const string SectionName = "ConfluentCluster";

    public string BrokerUrl { get; init; } = string.Empty;

    public string SchemaRegistryUrl { get; init; } = string.Empty;
}

public class ConfluentClusterOptionValidation : AbstractValidator<ConfluentOptions>
{
    public ConfluentClusterOptionValidation()
    {
        RuleFor(x => x.BrokerUrl).NotNull().NotEmpty();
        RuleFor(x => x.SchemaRegistryUrl).NotNull().NotEmpty();
    }
}
