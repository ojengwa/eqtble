"use client";

import {
  Dispatch,
  SetStateAction,
  useState,
} from 'react';

import { IForm } from '@/interface';
import {
  Box,
  Button,
  Container,
  Divider,
  forwardRef,
  HStack,
  Stack,
  Text,
} from '@chakra-ui/react';
import {
  FileUpload,
  FileUploadDropzone,
  FileUploadTrigger,
} from '@saas-ui/file-upload';
import {
  createField,
  Form,
  FormLayout,
  ObjectSchema,
} from '@saas-ui/forms';

import { SchemaDisplay } from './schema-display';

const schema = {
  body: {
    label: "Change Notes",
    name: "description",
    type: "textarea",
  },
} as const satisfies ObjectSchema;

interface Props {
  setData: Dispatch<SetStateAction<IForm>>;
  record: IForm;
}

const UploadField = createField(
  forwardRef((props, ref) => {
    const { onChange, callback, ...rest } = props;
    return (
      <FileUpload
        maxFileSize={1024 * 1024}
        accept=".yml,.yaml"
        {...rest}
        onFileChange={async (files) => {
          const [file] = files.acceptedFiles;
          callback(file);
          onChange(files.acceptedFiles);
        }}
        maxFiles={1}
        inputRef={ref}
      >
        {({ acceptedFiles, deleteFile }) => (
          <FileUploadDropzone>
            <Text fontSize="sm">Drag your YAML file here</Text>
            {!acceptedFiles?.length ? (
              <FileUploadTrigger as={Button}>Select file</FileUploadTrigger>
            ) : (
              <HStack>
                <Text fontSize="sm">{acceptedFiles[0].name}</Text>
                <Button
                  onClick={(e) => {
                    e.stopPropagation();
                    callback(undefined);
                    deleteFile(acceptedFiles[0]);
                  }}
                >
                  Clear
                </Button>
              </HStack>
            )}
          </FileUploadDropzone>
        )}
      </FileUpload>
    );
  }),
  {
    isControlled: true,
  }
);

export default function FormField({ record, setData }: Props) {
  const [file, setFile] = useState<File | undefined>(undefined);

  return (
    <Stack height="90vh" spacing={4} divider={<Divider />}>
      <Box>
        <Form
          schema={schema}
          onSubmit={(data) => console.log(data)}
          onChange={async (data) => {

            const _data = { ...record, ...data };

            if (data.file?.length) {
              const [_file] = data.file;
              setFile(_file);
              _data.name = _file?.name;
              _data.file = _file;
            } else {
              _data.file = undefined as unknown as File;
            }
            setData(_data as IForm);
          }}
        >
          {({ Field }) => (
            <FormLayout>
              <Field
                name="description"
                label="Change Note"
                placeholder={"Include commit notes, how-tos etc..."}
                type={"textarea"}
              />
              <UploadField
                name="file"
                label="Schema Definition File"
                callback={setFile}
              />
            </FormLayout>
          )}
        </Form>
      </Box>
      <Box flex={1}>
        <Container w="100%" justifyContent="flex-end"></Container>
        <SchemaDisplay file={file} />
      </Box>
    </Stack>
  );
}
