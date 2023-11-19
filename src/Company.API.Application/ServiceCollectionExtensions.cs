using Company.API.Application.Features.LongRunningOperations;
using Company.API.Application.Features.Session;
using Company.API.Application.Infrastructure;

using Microsoft.Extensions.DependencyInjection;
using FluentValidation;

using Company.API.Application.Validation;

using Microsoft.Extensions.Configuration;

namespace Company.API.Application;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplication(
        this IServiceCollection services,
        IConfiguration config
    )
    {
        services
            .AddOptions<ConfluentOptions>()
            .Bind(config.GetRequiredSection(ConfluentOptions.SectionName))
            .ValidateFluently()
            .ValidateOnStart();

        services
            .AddOptions<SessionOptions>()
            //            .Bind(config.GetRequiredSection(SessionOptions.SectionName))
            .ValidateFluently()
            .ValidateOnStart();

        services.AddValidatorsFromAssemblies(
            AppDomain.CurrentDomain.GetAssemblies(),
            lifetime: ServiceLifetime.Transient
        );

        services.AddMediatR(cfg =>
        {
            cfg.RegisterServicesFromAssemblies(AppDomain.CurrentDomain.GetAssemblies());
            cfg.AddOpenBehavior(typeof(ValidationBehavior<,>));
        });

        services.AddHostedService<BackgroundStatusWorker>();
        services.AddSchemaRegistry(config);
        services.AddConfluentFactory();

        return services;
    }
}
