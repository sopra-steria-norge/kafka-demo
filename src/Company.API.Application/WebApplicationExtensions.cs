using Microsoft.AspNetCore.Builder;
using Company.API.Application.Features.LongRunningOperations;
using Company.API.Application.Features.Session;
using Company.API.Application.Validation;

using Microsoft.AspNetCore.Http;

namespace Company.API.Application;

public static class WebApplicationExtensions
{
    public static WebApplication? MapApplication(this WebApplication? app)
    {
        app?.MapGroup("/long-operations").MapLongRunningOperations().WithTags("LongOperations");

        app?.MapGroup("/sessions").MapSession().WithTags("Session");

        return app;
    }

    public static WebApplication? UseValidationExceptionHandler(this WebApplication? app)
    {
        app?.UseMiddleware<ValidationExceptionHandlingMiddleware>();

        return app;
    }
}
