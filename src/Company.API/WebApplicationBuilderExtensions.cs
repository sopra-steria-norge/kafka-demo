using System.Diagnostics;
using System.Reflection;
using Azure.Monitor.OpenTelemetry.Exporter;
using OpenTelemetry.Logs;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

namespace Company.API;

internal static class WebApplicationBuilderExtensions
{
    public static string ConfiugrationDirectory = "Configurations";

    internal static WebApplicationBuilder AddConfiguration(this WebApplicationBuilder builder)
    {
        var env = builder.Environment;
        var config = builder.Configuration;

        config
            .AddJsonFile(
                $"{ConfiugrationDirectory}/appsettings.json",
                optional: false,
                reloadOnChange: true
            )
            .AddJsonFile(
                $"{ConfiugrationDirectory}/appsettings.{env.EnvironmentName}.json",
                optional: true,
                reloadOnChange: true
            )
            .AddJsonFile(
                $"{ConfiugrationDirectory}/logging.json",
                optional: false,
                reloadOnChange: true
            )
            .AddJsonFile(
                $"{ConfiugrationDirectory}/logging.{env.EnvironmentName}.json",
                optional: true,
                reloadOnChange: true
            )
            .AddJsonFile(
                $"{ConfiugrationDirectory}/telemetry.json",
                optional: false,
                reloadOnChange: true
            )
            .AddJsonFile(
                $"{ConfiugrationDirectory}/telemetry.{env.EnvironmentName}.json",
                optional: true,
                reloadOnChange: true
            )
            .AddJsonFile(
                $"{ConfiugrationDirectory}/confluent.json",
                optional: false,
                reloadOnChange: true
            )
            .AddJsonFile(
                $"{ConfiugrationDirectory}/confluent.{env.EnvironmentName}.json",
                optional: true,
                reloadOnChange: true
            )
            .AddJsonFile(
                $"{ConfiugrationDirectory}/session.json",
                optional: false,
                reloadOnChange: true
            )
            .AddJsonFile(
                $"{ConfiugrationDirectory}/session.{env.EnvironmentName}.json",
                optional: true,
                reloadOnChange: true
            )
            .AddJsonFile(
                $"{ConfiugrationDirectory}/topics.json",
                optional: false,
                reloadOnChange: true
            )
            .AddJsonFile(
                $"{ConfiugrationDirectory}/topics.{env.EnvironmentName}.json",
                optional: true,
                reloadOnChange: true
            )
            .AddEnvironmentVariables();

        return builder;
    }

    internal static WebApplicationBuilder AddOpenTelemetry(this WebApplicationBuilder builder)
    {
        if (builder.Configuration.GetValue<bool>("Telemetry:Enabled"))
        {
            var assembly = Assembly.GetExecutingAssembly();
            var version = assembly
                .GetCustomAttribute<AssemblyInformationalVersionAttribute>()
                ?.InformationalVersion;

            var resource = ResourceBuilder
                .CreateDefault()
                .AddTelemetrySdk()
                .AddService(
                    serviceName: assembly.GetName().Name
                        ?? throw new ArgumentNullException("Service name can not be null"),
                    serviceVersion: version
                );

            // Adding the OtlpExporter creates a GrpcChannel.
            // This switch must be set before creating a GrpcChannel when calling an insecure gRPC service.
            // See: https://docs.microsoft.com/aspnet/core/grpc/troubleshoot#call-insecure-grpc-services-with-net-core-client
            if (builder.Configuration.GetValue<bool>("Telemetry:Otlp:Enabled"))
                AppContext.SetSwitch(
                    "System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport",
                    true
                );

            builder.Services
                .AddOpenTelemetry()
                .WithTracing(b =>
                {
                    AppContext.SetSwitch("Azure.Experimental.EnableActivitySource", true);
                    Activity.DefaultIdFormat = ActivityIdFormat.W3C;

                    b.SetResourceBuilder(resource);
                    b.AddSource("Azure.*");
                    b.AddSource("Company.*");
                    b.AddHttpClientInstrumentation();
                    b.AddAspNetCoreInstrumentation();

                    if (builder.Configuration.GetValue<bool>("Telemetry:Console"))
                        b.AddConsoleExporter();

                    if (builder.Configuration.GetValue<bool>("Telemetry:Otlp:Enabled"))
                        b.AddOtlpExporter(
                            options =>
                                options.Endpoint = new Uri(
                                    builder.Configuration.GetValue<string>("Telemetry:Otlp:Url")
                                        ?? throw new ArgumentNullException(
                                            "Telemetry URL can not be null"
                                        )
                                )
                        );

                    if (builder.Configuration.GetValue<bool>("Telemetry:Azure:Enabled"))
                        b.AddAzureMonitorTraceExporter(
                            o =>
                                o.ConnectionString =
                                    builder.Configuration.GetValue<string>(
                                        "APPLICATIONINSIGHTS_CONNECTION_STRING"
                                    )
                                    ?? throw new ArgumentNullException(
                                        "Application Insight Connection string can not be null"
                                    )
                        );
                })
                .WithMetrics(b =>
                {
                    b.SetResourceBuilder(resource);
                    b.AddAspNetCoreInstrumentation();
                    b.AddHttpClientInstrumentation();

                    if (builder.Configuration.GetValue<bool>("Telemetry:Console"))
                        b.AddConsoleExporter();

                    if (builder.Configuration.GetValue<bool>("Telemetry:Otlp:Enabled"))
                        b.AddOtlpExporter(
                            options =>
                                options.Endpoint = new Uri(
                                    builder.Configuration.GetValue<string>("Telemetry:Otlp:Url")
                                        ?? throw new ArgumentNullException(
                                            "Telemetry URL can not be null"
                                        )
                                )
                        );
                    if (builder.Configuration.GetValue<bool>("Telemetry:Azure:Enabled"))
                        b.AddAzureMonitorMetricExporter(
                            o =>
                                o.ConnectionString =
                                    builder.Configuration.GetValue<string>(
                                        "APPLICATIONINSIGHTS_CONNECTION_STRING"
                                    )
                                    ?? throw new ArgumentNullException(
                                        "Application Insight Connection string can not be null"
                                    )
                        );
                });

            builder.Logging.AddOpenTelemetry(b =>
            {
                b.SetResourceBuilder(resource);
                b.IncludeFormattedMessage = true;
                b.IncludeScopes = true;
                b.ParseStateValues = true;

                if (builder.Configuration.GetValue<bool>("Telemetry:Console"))
                    b.AddConsoleExporter();

                // if (builder.Configuration.GetValue<bool>("Telemetry:Otlp:Enabled"))
                //     b.AddOtlpExporter(options => options.Endpoint = new Uri(builder.Configuration.GetValue<string>("Telemetry:Otlp:Url")));

                if (builder.Configuration.GetValue<bool>("Telemetry:Azure:Enabled"))
                    b.AddAzureMonitorLogExporter(
                        o =>
                            o.ConnectionString =
                                builder.Configuration.GetValue<string>(
                                    "APPLICATIONINSIGHTS_CONNECTION_STRING"
                                )
                                ?? throw new ArgumentNullException(
                                    "Application Insight Connection string can not be null"
                                )
                    );
            });
        }

        return builder;
    }
}
