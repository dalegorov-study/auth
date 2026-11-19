FROM --platform=$BUILDPLATFORM golang:1.24.8-alpine AS build

ARG TARGETOS
ARG TARGETARCH

# Псевдоверсия Go указывает на коммит тега RELEASE.2025-10-15T17-29-55Z.
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    source_module=github.com/minio/minio@v0.0.0-20251015172955-9e49d5e7a648 \
    && go mod download "$source_module" \
    && cd "/go/pkg/mod/$source_module" \
    && mkdir -p /out/licenses \
    && cp LICENSE CREDITS /out/licenses/ \
    && release_flags='-s -w \
        -X github.com/minio/minio/cmd.Version=2025-10-15T17:29:55Z \
        -X github.com/minio/minio/cmd.ReleaseTag=RELEASE.2025-10-15T17-29-55Z \
        -X github.com/minio/minio/cmd.CommitID=9e49d5e7a648f00e26f2246f4dc28e6b07f8c84a \
        -X github.com/minio/minio/cmd.ShortCommitID=9e49d5e7a648 \
        -X github.com/minio/minio/cmd.CopyrightYear=2025' \
    && CGO_ENABLED=0 GOOS="$TARGETOS" GOARCH="$TARGETARCH" \
        go build -mod=readonly -tags kqueue -trimpath -ldflags "$release_flags" -o /out/minio .

FROM alpine:3.24

RUN apk add --no-cache ca-certificates curl \
    && addgroup -S minio \
    && adduser -S -G minio minio \
    && install -d -o minio -g minio /data
COPY --from=build /out/licenses/ /licenses/
COPY --from=build /out/minio /usr/local/bin/minio

USER minio
EXPOSE 9000
ENTRYPOINT ["/usr/local/bin/minio"]
CMD ["server", "/data"]
