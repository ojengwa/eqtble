import { FiAlertOctagon } from 'react-icons/fi';

import { IRecord } from '@/interface';
import {
  Box,
  Card,
  CardBody,
  CardHeader,
  Center,
  Heading,
  Progress,
  Text,
} from '@chakra-ui/react';
import {
  EmptyState,
  Property,
  PropertyList,
} from '@saas-ui/react';

interface SchemaDetailsProps {
  schema?: IRecord;
}

export default function SchemaDetails({ schema }: SchemaDetailsProps) {
  return (
    <Card shadow={"none"} border={"none"}>
      <CardHeader display="flex" flexDirection="row">
        <Heading size="sm">Schema Details</Heading>
      </CardHeader>
      <CardBody>
        {schema ? (
          <PropertyList>
            <Property
              label="Billing plan"
              value={<Text fontWeight="bold">Professional</Text>}
            />
            <Property label="Billing period" value="Yearly" />
            <Property label="Renewal date" value="01-01-2023" />
            <Property
              label="Users"
              value={
                <Box flex="1">
                  <Text fontSize="sm">20/100</Text>{" "}
                  <Progress
                    value={20}
                    size="xs"
                    colorScheme="primary"
                    borderRadius="full"
                  />
                </Box>
              }
            />
            <Property label="Price" value="€1250,-" />
          </PropertyList>
        ) : (
          <Center p="4">
            <EmptyState
              size={"md"}
              variant={"centered"}
              colorScheme={"red"}
              icon={FiAlertOctagon}
              title="No schema selected"
              description="You haven't selected any schema yet."
            />
          </Center>
        )}
      </CardBody>
    </Card>
  );
}
