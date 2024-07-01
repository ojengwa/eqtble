import { IRecord } from '@/interface';
import {
  Box,
  Center,
  Grid,
  GridItem,
  Text,
  VStack,
} from '@chakra-ui/react';
import {
  Navbar,
  NavbarContent,
  NavbarItem,
} from '@saas-ui/react';

import api from '../../lib/api';
import { FileIcon } from './_components/icons';
import SchemaButton from './_components/schema-button';

export default async function Page() {
  let data: Array<IRecord> = [];
  let error: string | null = null;

  try {
    const result = await api.get("/schemas/");
    data = result.data as Array<IRecord>;
  } catch (err) {
    error = (err as Error).message;
  }

  return (
    <Box>
      <Navbar position="sticky" borderBottomWidth="1px" mb={8}>
        <NavbarContent justifyContent="flex-end" spacing="2">
          <NavbarItem>{/* <Button href="#">Login</Button> */}</NavbarItem>
          <SchemaButton />
        </NavbarContent>
      </Navbar>

      <Box p={4}>
        {data?.length ? (
          <Grid templateColumns="repeat(auto-fill, minmax(150px, 1fr))" gap={6}>
            {data.map((file, key) => (
              <GridItem
                key={key}
                cursor={"pointer"}
                borderWidth="1px"
                borderRadius="md"
                overflow="hidden"
                p={2}
                display="flex"
                flexDirection="column"
                alignItems="center"
                textAlign="center"
                backgroundColor="white"
                _hover={{ boxShadow: "sm" }}
              >
                <FileIcon />
                <VStack spacing={2}>
                  <Text fontWeight="bold">{file.name}</Text>
                  <Text fontSize="sm" color="gray.500">
                    Revisions: {file.revisions}
                  </Text>
                </VStack>
              </GridItem>
            ))}
          </Grid>
        ) : (
          <Center py={10}>No schema saved yet.</Center>
        )}
      </Box>
    </Box>
  );
}
