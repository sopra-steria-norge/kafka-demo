using System.Text.Json.Serialization;

using Company.API;
using Company.API.Application;

using Microsoft.AspNetCore.Mvc.Versioning;
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

builder.AddConfiguration();
builder.AddOpenTelemetry();

builder.Services.AddRouting(options => options.LowercaseUrls = true);

// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.UseInlineDefinitionsForEnums();
    c.SwaggerDoc(
        "v1",
        new OpenApiInfo()
        {
            Title = "Kafka/Confluent Demo",
            Version = "v1",
            Description = "Lets use this to test Kafka/Confluent"
        }
    );

    var assembly = typeof(Program).Assembly.GetName();
    var xmlFile = $"{assembly.Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    if (File.Exists(xmlPath))
    {
        c.IncludeXmlComments(xmlPath);
    }
});

builder.Services.AddApiVersioning(options =>
{
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
    options.ApiVersionReader = ApiVersionReader.Combine(
        new HeaderApiVersionReader("Api-Version"),
        new MediaTypeApiVersionReader("version"),
        new QueryStringApiVersionReader("api-version")
    );
});

builder.Services.AddHealthChecks();

builder.Services
    .AddControllers()
    .AddJsonOptions(
        options => options.JsonSerializerOptions.Converters.Add(new JsonStringEnumConverter())
    );

builder.Services.AddMemoryCache();
builder.Services.AddApplication(builder.Configuration);

var app = builder.Build();

app.UseRouting();

app.UseSwagger(c => c.RouteTemplate = "docs/{documentname}/swagger.json");

// Add our custom validation exception handler
app.UseValidationExceptionHandler();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment() || app.Environment.IsEnvironment("Test"))
{
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/docs/v1/swagger.json", "v1 - dev");
        c.RoutePrefix = "docs";
    });
}
else if (app.Environment.IsProduction())
{
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/docs/v1/swagger.json", "v1");
        c.SupportedSubmitMethods();
        c.RoutePrefix = "docs";
        c.EnableTryItOutByDefault();
    });
}

app.UseHttpsRedirection();

app.MapHealthChecks("/healthz");

app.MapApplication();

app.Run();

// Makes the Program available to testing
public partial class Program { }
