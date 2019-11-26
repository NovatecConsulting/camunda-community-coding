package de.novatec;

import org.camunda.bpm.spring.boot.starter.annotation.EnableProcessApplication;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@EnableProcessApplication
public class MyServiceApplication {

    public static void main(String... args) {
        SpringApplication.run(MyServiceApplication.class, args);
    }

}