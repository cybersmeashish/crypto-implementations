# A post-quantum migration needs an evidence trail

## Scope before selection

Inventory the protocol or artifact, cryptographic purpose, algorithm and parameters, implementation or supplier, owner, data lifetime, and upgrade mechanism. A certificate, transport protocol, signing process, and stored ciphertext may have different migration dependencies.

This is an original reference workflow. It uses the NIST standards linked in the [repository introduction](../README.md) as primary technical sources.

## Decisions and required evidence

| Decision | Evidence to collect | Unresolved question |
| --- | --- | --- |
| Prioritize a confidentiality dependency | Data retention and required secrecy period; current key-establishment path | How long must captured information remain confidential? |
| Change a transport integration | Protocol support, counterpart compatibility, measured message sizes and handshake behavior | Which supplier or client cannot upgrade on the same schedule? |
| Change a signing path | Signature verification support, artifact retention, key custody, rollback and archival policy | Must older artifacts remain verifiable after the migration? |
| Evaluate a PQC-labelled component | Exact implementation, revision, parameters, test vectors, assurance status and integration tests | What has been verified beyond the algorithm name? |
| Approve production adoption | Failure behavior, performance under realistic load, observability, operational ownership and recovery | Can the system recover without silently downgrading its security policy? |

ML-KEM addresses key encapsulation. ML-DSA and SLH-DSA address signatures. These standards serve different purposes and are not interchangeable application controls.

## Staged research

1. **Inventory:** locate dependencies and ownership gaps.
2. **Compatibility study:** document protocol and supplier constraints.
3. **Bounded benchmark:** record environment, implementation revision, parameters, baseline, latency distribution, payload sizes, and failure cases.
4. **Integration evaluation:** verify the actual protocol and application behavior.
5. **Operational decision:** record owners, rollout criteria, recovery, and the remaining risks.

Only the inventory review lab is implemented here. Compatibility studies, cryptographic benchmarks, and deployment validation remain future work.
