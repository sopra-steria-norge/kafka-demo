using System.Text;
using Confluent.Kafka;
using CloudNative.CloudEvents;
using CloudNative.CloudEvents.Extensions;

namespace Company.API.Application.CloudEvents;

public static class CloudEventsExtensions
{
    public static CloudEventAttribute CorrelationId { get; } =
        CloudEventAttribute.CreateExtension("correlationid", CloudEventAttributeType.String);

    public static CloudEvent SetCorrelationId(this CloudEvent ce, Guid correlationid)
    {
        ce[CorrelationId] = correlationid.ToString();
        return ce;
    }

    public static Headers MapHeaders(this CloudEvent ce)
    {
        var headers = new Headers
        {
            { "ce_specversion", Encoding.UTF8.GetBytes(ce.SpecVersion.VersionId) }
        };

        foreach (var pair in ce.GetPopulatedAttributes())
        {
            var attribute = pair.Key;
            if (
                attribute == ce.SpecVersion.DataContentTypeAttribute
                || attribute.Name == Partitioning.PartitionKeyAttribute.Name
            )
                continue;

            var value = attribute.Format(pair.Value);
            headers.Add($"ce_{attribute.Name}", Encoding.UTF8.GetBytes(value));
        }

        return headers;
    }
}
