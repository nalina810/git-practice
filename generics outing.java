class genericsorting<T extends Comparable<T>>
{
T []a;
genericsorting(T[]a)
{
this.T []a=T []a;
}
void sorting()
{
T temp;
for(int i=0;i<a.length-1;i++)
{
for(int j=i;j<a.length-i-1;j++)
{
temp=a[j];
a[j]=a[j+1];
a[j+1]= temp;
}
}
void display()
{
for(int i=0;i<a.length-1;i++)
{
System.out.println("Sorted Array" + a[i]);
}
}
public static void main(String[]args)
{
Integer a[]={50,40,20,30,10};
genericsorting <Integer> gs1=new genericsorting<Integer>(a);
}
}