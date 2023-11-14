using MediatR;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;
using Microsoft.AspNetCore.Mvc;

namespace Company.API.Application.Features.LongRunningOperations;

public static class RouteGroupBuilderExtensions
{
    public static RouteGroupBuilder MapLongRunningOperations(this RouteGroupBuilder group)
    {
        group
            .MapGet(
                "/{id:Guid}",
                async ([FromServices] IMediator mediator, Guid id) =>
                {
                    var request = new LongOperationRequest { OperationId = id };
                    var result = await mediator.Send(request);

                    return result.Match(Results.Ok, Results.NotFound);
                }
            )
            .WithName("LongOperationStatus")
            .Produces<LongOperationResponse>()
            .ProducesProblem(StatusCodes.Status400BadRequest)
            .ProducesProblem(StatusCodes.Status404NotFound)
            .WithOpenApi(
                operation =>
                    new(operation)
                    {
                        Summary = "Retrive Long Operation status",
                        Description =
                            "Retrive the status of and long operation that has been started"
                    }
            );

        return group;
    }
}
