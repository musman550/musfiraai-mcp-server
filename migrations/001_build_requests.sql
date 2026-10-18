create table if not exists public.build_requests (
  id text primary key,
  name text not null,
  contact text not null,
  contact_key text not null,
  need text not null,
  status text not null default 'Received',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists build_requests_contact_key_created_idx
  on public.build_requests (contact_key, created_at desc);

-- RLS on with no policies: anon/public keys cannot read or write.
-- The server uses SUPABASE_SERVICE_KEY, which bypasses RLS.
alter table public.build_requests enable row level security;
