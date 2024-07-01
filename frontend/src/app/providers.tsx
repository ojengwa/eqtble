"use client";

import React from 'react';

import Link, { LinkProps } from 'next/link';
import { usePathname } from 'next/navigation';
import {
  FiDatabase,
  FiSearch,
} from 'react-icons/fi';

import {
  Box,
  Skeleton,
} from '@chakra-ui/react';
import {
  AppShell,
  ModalsProvider,
  NavItem,
  SaasProvider,
  Sidebar,
  SidebarSection,
  SidebarToggleButton,
} from '@saas-ui/react';

const NextLink = React.forwardRef<HTMLAnchorElement, LinkProps>(
  function NextLink(props, ref) {
    return <Link ref={ref} {...props} />;
  }
);
NextLink.displayName = "NextLink";

export function Providers({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  const onError = React.useCallback((error: Error) => {
    console.log(error);
  }, []);

  return (
    <SaasProvider linkComponent={NextLink} onError={onError}>
      <React.Suspense fallback={<Skeleton />}>
        <ModalsProvider>
          <AppShell
            variant="static"
            minH="$100vh"
            sidebar={
              <Sidebar toggleBreakpoint="sm">
                <SidebarToggleButton />
                <SidebarSection aria-label="Main">
                  <NavItem
                    icon={<FiSearch />}
                    href="/"
                    isActive={pathname === "/"}
                  >
                    Query Builder
                  </NavItem>
                  <NavItem
                    icon={<FiDatabase />}
                    href="/schemas"
                    isActive={pathname === "/schemas"}
                  >
                    Schemas
                  </NavItem>
                </SidebarSection>
              </Sidebar>
            }
          >
            <Box as="main" flex="1" py="2" px="4">
              {children}
            </Box>
          </AppShell>
        </ModalsProvider>
      </React.Suspense>
    </SaasProvider>
  );
}
