'use client';

import { RefreshCwIcon } from '@/components/ui/Icons';

interface TransformButtonProps {
  onClick: () => void;
  disabled?: boolean;
  loading?: boolean;
}

export function TransformButton({ onClick, disabled = false, loading = false }: TransformButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className="btn-primary w-full flex items-center justify-center py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {loading ? (
        <>
          <RefreshCwIcon className="h-5 w-5 mr-2 animate-spin" />
          Transforming...
        </>
      ) : (
        "Transform Color"
      )}
    </button>
  );
}
