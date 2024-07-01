"use client";
import {
  useEffect,
  useState,
} from 'react';

import { FiFileText } from 'react-icons/fi';

import {
  Card,
  Center,
  Code,
} from '@chakra-ui/react';
import { EmptyState } from '@saas-ui/react';

interface SchemaDisplayProps {
  file?: File;
}

export function SchemaDisplay({ file }: SchemaDisplayProps) {
  const [content, setContent] = useState<string | null>(null);

  useEffect(() => {
    async function getContent() {
      const _content = (await file?.text()) || null;
      setContent(_content);
    }
    getContent();
  }, [file]);

  return (
    <>
      {content ? (
        <Card>
            <Code whiteSpace="pre" p={4}>{content}</Code>
        </Card>
      ) : (
        <Center py={10}>
          <EmptyState
            size={"md"}
            variant={"centered"}
            icon={FiFileText}
            title="No file selected"
            description="You haven't selected any schema file yet yet."
          />
        </Center>
      )}
    </>
  );
}
