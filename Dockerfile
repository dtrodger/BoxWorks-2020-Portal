FROM python:3.8
 WORKDIR /home/box_platform_portal 
ENV FLASK_APP "src/main:flask_app" 
COPY . .
RUN groupadd docker && \
      useradd -m -g docker docker && \
      chown -R docker:docker /home/box_platform_portal && \
      python -m pip install --upgrade pip && \
      pip install -r requirements.txt 
EXPOSE 5000
USER docker 
CMD ["flask", "run", "-h", "0.0.0.0"] 