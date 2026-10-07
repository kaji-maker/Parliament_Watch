import assert from "node:assert/strict";
import test from "node:test";
import { fetchPublicationStatus, parseStatus } from "../src/lib/status.ts";

test("only the explicit Phase 1 pending contract is accepted", () => {
  assert.deepEqual(parseStatus({ phase: 1, publication_status: "verification_pending" }), { kind: "verification_pending" });
  for (const value of [null, [], {}, { status: "Online" }, { phase: 1, publication_status: "live" }, { phase: 2, publication_status: "verification_pending" }]) {
    assert.deepEqual(parseStatus(value), { kind: "unavailable" });
  }
});

test("an HTTP error never becomes an empty or verified dataset", async () => {
  const state = await fetchPublicationStatus("https://backend.example/status", async () => new Response("[]", { status: 503 }));
  assert.deepEqual(state, { kind: "unavailable" });
});

test("connection failures and invalid JSON remain unavailable", async () => {
  assert.deepEqual(await fetchPublicationStatus("https://backend.example/status", async () => { throw new Error("offline"); }), { kind: "unavailable" });
  assert.deepEqual(await fetchPublicationStatus("https://backend.example/status", async () => new Response("not JSON")), { kind: "unavailable" });
});

test("successful metadata does not supply synthetic records", async () => {
  const state = await fetchPublicationStatus("https://backend.example/status", async (_url, options) => {
    assert.equal(options.cache, "no-store");
    assert.equal(options.redirect, "error");
    assert.ok(options.signal);
    return Response.json({ phase: 1, publication_status: "verification_pending" });
  });
  assert.deepEqual(state, { kind: "verification_pending" });
});

