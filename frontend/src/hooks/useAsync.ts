import { useState, useEffect, useCallback, useRef } from 'react';

export interface UseAsyncState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

export function useAsync<T>(
  asyncFunction: () => Promise<T>,
  immediate = true
): UseAsyncState<T> & { execute: () => Promise<void> } {
  const [state, setState] = useState<UseAsyncState<T>>({
    data: null,
    loading: immediate,
    error: null,
  });

  // Keep a ref to the async function so we don't recreate the `execute`
  // callback each render if the caller didn't memoize the function.
  const asyncFnRef = useRef(asyncFunction);
  useEffect(() => {
    asyncFnRef.current = asyncFunction;
  }, [asyncFunction]);

  const execute = useCallback(async () => {
    setState({ data: null, loading: true, error: null });
    try {
      const response = await asyncFnRef.current();
      setState({ data: response, loading: false, error: null });
    } catch (error) {
      setState({ data: null, loading: false, error: error as Error });
    }
  }, []);

  // Track the last function executed so we only re-run when the function truly changes.
  // Initialize to null so the first mount will always execute when `immediate` is true.
  const lastExecutedFnRef = useRef<typeof asyncFnRef.current | null>(null);

  useEffect(() => {
    if (immediate) {
      // If the async function reference changed since we last executed, run it.
      if (asyncFnRef.current !== lastExecutedFnRef.current) {
        lastExecutedFnRef.current = asyncFnRef.current;
        execute();
      }
    }
    // Include the original asyncFunction in deps so this effect runs when the
    // caller provides a new function (e.g., fetch callback memoized with
    // changing parameters like `dimension`). Callers should memoize their
    // fetch functions with `useCallback` to avoid unnecessary re-runs.
  }, [immediate, execute, asyncFunction]);

  return { ...state, execute };
}
