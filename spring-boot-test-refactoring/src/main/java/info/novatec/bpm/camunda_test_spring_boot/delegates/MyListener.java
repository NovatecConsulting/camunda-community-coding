package info.novatec.bpm.camunda_test_spring_boot.delegates;

import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.ExecutionListener;

public class MyListener implements ExecutionListener {

    @Override
    public void notify(DelegateExecution execution) throws Exception {
        // TODO Auto-generated method stub
        System.out.println("hi!");

    }
}
