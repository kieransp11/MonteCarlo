#include <vector>
#include <stdexcept>

template<class T>
T get_max(T a, T b)
{
    return (a>b)? a : b;
}

template<class T>
class Stack
{
    private:
        std::vector<T> elems;

    public:
        Stack(){};
        Stack(std::vector<T> initial_items) : 
            elems(initial_items) {};

        void push(const T ele);

        T pop();

        T peek() const;

        bool empty() const {
            return elems.empty();
        };

        int height() const {
            return elems.size();
        };
};

template<class T>
void Stack<T>::push(const T ele) {
    elems.push_back(ele);
}

template<class T>
T Stack<T>::pop() {
    const auto result = Stack<T>::peek();
    elems.pop_back();
    return result;
}

template<class T>
T Stack<T>::peek() const {
    if (elems.empty()){
        throw std::out_of_range("Stack<>::peek(): empty stack");
    }
    return elems.back();    
}