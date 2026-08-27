# python-ai-sessions
Sessions for Python and AI

## Authentication

The `/users` and `/policies` endpoints require a Supabase access token:

```text
Authorization: Bearer <supabase-access-token>
```

Set these environment variables before starting the API:

```text
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
```

Get a token by signing users up or in with Supabase Auth, for example with
`supabase.auth.signInWithPassword(...)` in a frontend. Send the returned
`access_token` in the `Authorization` header for API requests.
