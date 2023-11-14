using Confluent.Kafka;

namespace Company.API.Application.Infrastructure.Confluent;

public interface IAdminFactory
{
    IAdminClient GetAdminClient();
}
