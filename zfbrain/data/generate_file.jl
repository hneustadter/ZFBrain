#f(θ,t,tmax) = ((t+1)*cos(θ),(t+1)*sin(θ),t/tmax)
f(θ,t,tmax) = (t/tmax*(t/tmax-1)*cos(θ),t/tmax*(t/tmax-1)*sin(θ),t/tmax)

function generate_data()
    # L=3, N=4 is test case in notes
    L = 8
    N = 20
    io=open("test_surface.surf","w")
    println(io,"example of data file from slice")
    println(io,L," ",N)
    for ti=0:(L-1)
        for tj=1:N
            θ = (tj-1)*2*pi/N
            x,y,z = f(θ,ti,L-1)
            println(io,x," ",y," ",z)
        end

    end

    close(io)
end

generate_data()