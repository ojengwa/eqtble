"use client";

import {
  useEffect,
  useState,
} from 'react';

import {
  IForm,
  IRecord,
} from '@/interface';
import api from '@/lib/api';
import {
  Button,
  DrawerFooter,
} from '@chakra-ui/react';
import {
  NavbarItem,
  useModals,
  useSnackbar,
} from '@saas-ui/react';

import SchemaDrawer from './drawer';

interface Props {
  schema?: IRecord;
}

export default function SchemaButton({ schema }: Props) {
  const modals = useModals();
  const snackbar = useSnackbar();
  const [data, setData] = useState<IForm>({} as IForm);
  const [isValid, setIsValid] = useState<boolean>(false);
  const [isCreating, setIsCreating] = useState<boolean>(false);

  async function handleSubmit() {
    try {
      setIsCreating(true);
      const formData = new FormData();
      formData.append("name", data.name);
      formData.append("description", data.description);
      formData.append("file", data.file);
      const response = await api.post("/schemas/", formData);
      console.log(response, "response");
    } catch (err: any) {
      snackbar({
        title: "Schema Creation Failed.",
        description: err.message,
        status: "error",
        isClosable: true,
      });
    } finally {
      setIsCreating(false);
    }
  }

  useEffect(() => {
    if (!data.name) {
      setIsValid(false);
    }
    for (const key in data) {
      if (!data[key]) {
        setIsValid(false);
        return;
      }
    }
    setIsValid(true);
  }, [data]);

  return (
    <NavbarItem>
      <Button
        onClick={() =>
          modals.drawer({
            title: "Schema Definition",
            body: <SchemaDrawer setData={setData} data={data as IForm} />,
            footer: (
              <DrawerFooter>
                <Button
                  onClick={() => handleSubmit()}
                  isDisabled={!isValid}
                  isLoading={isCreating}
                  loadingText="Submitting"
                >
                  Submit Schema
                </Button>
              </DrawerFooter>
            ),
            isFullHeight: true,
            size: "full",
          })
        }
      >
        Add Schema
      </Button>
    </NavbarItem>
  );
}
