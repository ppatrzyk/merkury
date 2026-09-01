LABEL org.opencontainers.image.source="https://github.com/ppatrzyk/merkury"

FROM docker.io/library/python:3.14.2-trixie AS python-build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /merkury
COPY . /merkury
RUN pip3 install .[server]

FROM docker.io/library/python:3.14.2-slim-trixie AS final-image

COPY --from=python-build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000
CMD ["merkury", "--author", "merkury", "--server", "0.0.0.0:8000", "server", "/etc/merkury/scripts"]
