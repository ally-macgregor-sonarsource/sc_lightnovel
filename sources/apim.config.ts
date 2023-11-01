import { DPCApiConfig, DPCApimConfig, DPCBackendService, DPCOperations } from '@dpc-odg/libs-iac-apps';
import { Config as PulumiConfig } from '@pulumi/pulumi/config';
import { Input, interpolate } from '@pulumi/pulumi/output';

const pulumiConfig = new PulumiConfig('env');
const apimTransactionTypeGetCachingDuration = pulumiConfig.requireObject<number>(
  'get-dashboard-configurations-caching-duration'
);

const cacheLookupPolicy = `<cache-lookup vary-by-developer="false" vary-by-developer-groups="false" downstream-caching-type="none" must-revalidate="true" caching-type="internal" />`;

const cacheStorePolicy = (duration: number): string => {
  return `
  <choose>
    <when condition="@(context.Response.StatusCode == 200)">
      <cache-store duration="${duration}" />
    </when>
  </choose>`;
};

export const apimConfig = (functionName: Input<string>): DPCApimConfig => {
  const operations: DPCOperations[] = [
    {
      operationId: 'get-configurations-v1',
      displayName: 'get-configurations-v1',
      method: 'GET',
      templateParameters: [],
      urlTemplate: '/v1/configurations',
      xmlContent: interpolate`<policies>
      <inbound>
        <base />
        <set-backend-service id="apim-generated-policy" backend-id="${functionName}" />
        ${cacheLookupPolicy}
      </inbound>
      <outbound>
          <base />
          ${cacheStorePolicy(apimTransactionTypeGetCachingDuration)}
      </outbound>
    </policies>`,
    },
  ];

  const apiConfig: DPCApiConfig[] = [
    {
      apiRevision: '1',
      description: '',
      displayName: 'oss-dashboard-api',
      name: 'oss-dashboard-api',
      path: 'dashboard',
      protocols: ['https'],
      subscriptionKeyParameterNames: {
        header: 'Ocp-Apim-Subscription-Key',
        query: 'subscription-key',
      },
      subscriptionRequired: true,
      productName: ['oss-dashboard-public'],
      xmlContent: `<policies></policies>`,
      operations: operations,
    },
  ];
  const backends: DPCBackendService[] = [
    {
      backendType: 'function-app',
      pulumiShortName: 'dashboard-api',
    },
  ];

  const apimConfigValues: DPCApimConfig = {
    apis: apiConfig,
    backends: backends,
  };
  return apimConfigValues;
};
