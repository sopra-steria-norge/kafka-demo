using System.Collections.Concurrent;

namespace Company.API.Application.Infrastructure;

public class MemoryOperationStorage : IMemoryOperationStorage
{
    private readonly ConcurrentDictionary<string, byte> _storage = new();

    public void AddOperationId(string id)
    {
        _storage.TryAdd(id, 0);
    }

    public IEnumerable<string> GetOperationIds()
    {
        return _storage.Keys;
    }
}
