namespace Company.API.Application.Infrastructure;

public interface IMemoryOperationStorage
{
    void AddOperationId(string id);

    IEnumerable<string> GetOperationIds();
}
