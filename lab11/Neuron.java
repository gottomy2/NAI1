import java.lang.Math.*;
import java.lang.reflect.Method;

public class Neuron {
    int[] weight;
    int bias;

    public Neuron(int[] weight, int bias){
        this.weight=weight;
        this.bias=bias;
    }

    public double output(int[] input,NeuronInterface neuronInterface){
        double output =0.00;
        for(int i=0;i<weight.length;i++){
            output+= weight[i] * input[i];
        }
        return neuronInterface.activation(output+bias);
    }
}
