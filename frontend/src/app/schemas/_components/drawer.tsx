import {
  Dispatch,
  SetStateAction,
} from 'react';

import {
  IForm,
  IRecord,
} from '@/interface';
import {
  Box,
  Divider,
  Stack,
} from '@chakra-ui/react';

import SchemaDetails from './details';
import FormField from './form';

interface Props {
  schema?: IRecord;
  setData: Dispatch<SetStateAction<IForm>>;
  data: IForm;
}

export default function SchemaDrawer({ schema, setData, data }: Props) {

  return (
    <>
      <Divider orientation={"horizontal"} />
      <Stack
        direction={{ base: "column", md: "row" }}
        spacing={8}
        height={"100vh"}
        py={8}
        divider={<Divider orientation="vertical" />}
      >
        <Box flex={3} minWidth={0}>
          <SchemaDetails />
        </Box>
        <Box flex={5} minWidth={0}>
          <FormField setData={setData} record={data} />
        </Box>
      </Stack>
    </>
  );
}
