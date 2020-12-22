public class Main {
    public static class Activation implements NeuronInterface{
        @Override
        public double activation(double x) {
            return 1 / (1 + Math.exp(-x));
        }
    }

    public static void main(String[] args){
        int[] weight = {0,1};
        Neuron neuron = new Neuron(weight,4);
        int[] input = {2,3};
        Activation activation = new Activation();
        double output = neuron.output(input,activation);
        System.out.println(output);
    }
}