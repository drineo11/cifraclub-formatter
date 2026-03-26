'use client';

import { useState } from 'react';

type LoadingStage = '' | 'downloading' | 'processing' | 'generating';

function validateUrl(url: string): string | null {
  if (!url) return null;
  try {
    const parsed = new URL(url);
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      return 'URL deve começar com http:// ou https://';
    }
    if (!parsed.hostname.includes('cifraclub.com.br')) {
      return 'URL deve ser do Cifra Club (cifraclub.com.br)';
    }
    return null;
  } catch {
    return 'URL inválida';
  }
}

export default function Home() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState<LoadingStage>('');
  const [urlError, setUrlError] = useState('');
  const [error, setError] = useState('');

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setUrl(value);
    if (value) {
      setUrlError(validateUrl(value) || '');
    } else {
      setUrlError('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const validationError = validateUrl(url);
    if (validationError) {
      setUrlError(validationError);
      return;
    }

    setLoading('downloading');
    setError('');
    setUrlError('');

    try {
      setLoading('processing');
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, format: 'docx' }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Erro ao gerar cifra');
      }

      setLoading('generating');
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;

      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = 'cifra.docx';
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
        if (filenameMatch && filenameMatch[1]) {
          filename = filenameMatch[1];
        }
      }

      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(downloadUrl);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Erro desconhecido';
      setError(message);
    } finally {
      setLoading('');
      setUrl('');
    }
  };

  const loadingMessages: Record<LoadingStage, string> = {
    '': 'Gerar Arquivo',
    downloading: 'Baixando cifra...',
    processing: 'Processando conteúdo...',
    generating: 'Gerando arquivo...',
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
      <div className="w-full max-w-lg bg-gray-800/50 backdrop-blur-md border border-gray-700 rounded-2xl shadow-2xl p-8 md:p-10">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-500 mb-2">
            Cifra Club Formatter
          </h1>
          <p className="text-gray-400 text-lg">
            Transforme cifras online em arquivos prontos para impressão
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="space-y-3">
            <label htmlFor="url" className="block text-lg font-medium text-gray-300">
              URL da Cifra
            </label>
            <div className="relative">
              <input
                type="url"
                id="url"
                required
                placeholder="https://www.cifraclub.com.br/..."
                value={url}
                onChange={handleUrlChange}
                className={`w-full pl-4 pr-4 py-4 bg-gray-900/80 border rounded-xl focus:ring-2 focus:border-transparent outline-none transition-all text-lg placeholder-gray-500 text-white shadow-inner ${
                  urlError ? 'border-red-500 focus:ring-red-500' : 'border-gray-600 focus:ring-orange-500'
                }`}
              />
            </div>
            {urlError && (
              <p className="text-red-400 text-sm flex items-center mt-1">
                <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {urlError}
              </p>
            )}
          </div>

          {error && (
            <div className="p-4 bg-red-900/30 border border-red-800 text-red-200 text-base rounded-xl flex items-center">
              <svg className="w-6 h-6 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading !== ''}
            className="w-full bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-500 hover:to-red-500 text-white font-bold py-4 px-6 rounded-xl transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none shadow-lg shadow-orange-900/20 flex items-center justify-center text-lg"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {loadingMessages[loading]}
              </>
            ) : (
              loadingMessages['']
            )}
          </button>
        </form>

        <p className="mt-8 text-center text-sm text-gray-500">
          Cole o link de uma cifra do Cifra Club para gerar uma versão formatada em uma única página.
        </p>
      </div>
    </main>
  );
}
