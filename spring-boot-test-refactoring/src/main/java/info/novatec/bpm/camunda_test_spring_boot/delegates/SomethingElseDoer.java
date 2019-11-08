package info.novatec.bpm.camunda_test_spring_boot.delegates;

import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.springframework.stereotype.Component;

@Component
public class SomethingElseDoer implements JavaDelegate {

    @Override
    public void execute(DelegateExecution execution) throws Exception {
        System.out.print("Real Delegate says hello!");

    }

}
