using Microsoft.AspNetCore.Routing;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using MediatR;

namespace Company.API.Application.Features.Session;

public static class RouteGroupBuilderExtensions
{
    public static RouteGroupBuilder MapSession(this RouteGroupBuilder group)
    {
        group
            .MapPost(
                "/",
                async (
                    [FromServices] IMediator mediator,
                    [FromBody] SessionRequest sessionRequest,
                    CancellationToken cancellationToken
                ) =>
                {
                    var result = await mediator.Send(sessionRequest, cancellationToken);

                    return result.Match(
                        response =>
                            Results.Accepted($"/long-operations/{response.OperationId}", response),
                        Results.BadRequest
                    );
                }
            )
            .WithName("SessionRequest")
            .Produces(StatusCodes.Status202Accepted, typeof(SessionResponse))
            .ProducesProblem(StatusCodes.Status400BadRequest)
            .WithOpenApi(
                operation =>
                    new(operation)
                    {
                        Summary = "Request an F1 session to be processed",
                        Description =
                            "Starts an long running opperation to get data from an F1 session",
                    }
            );

        return group;
    }
}
