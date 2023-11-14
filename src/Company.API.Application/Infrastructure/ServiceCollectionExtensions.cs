using Confluent.SchemaRegistry;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Company.API.Application.Infrastructure.Confluent;
using Company.API.Application.Infrastructure.Producer;
using Company.API.Application.Infrastructure.Consumer;

namespace Company.API.Application.Infrastructure;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddSchemaRegistry(
        this IServiceCollection services,
        IConfiguration config
    )
    {
        var schemaregistryConfig = new SchemaRegistryConfig
        {
            Url = config.GetValue<string>($"{ConfluentOptions.SectionName}:SchemaRegistryUrl")
        };

        services.AddSingleton<ISchemaRegistryClient>(
            new CachedSchemaRegistryClient(schemaregistryConfig)
        );
        return services;
    }

    public static IServiceCollection AddConfluentFactory(this IServiceCollection services)
    {
        services.AddSingleton<ConfluentFactory>();
        services.AddSingleton<IProducerFactory>(x => x.GetRequiredService<ConfluentFactory>());
        services.AddSingleton<IConsumerFactory>(x => x.GetRequiredService<ConfluentFactory>());
        services.AddSingleton<IAdminFactory>(x => x.GetRequiredService<ConfluentFactory>());

        return services;
    }
}
