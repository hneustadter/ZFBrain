f(θ,t) = ((t+1)*cos(θ),(t+1)*sin(θ),t)

function generate_data()
    for ti=1:3
        println(ti)
        for tj=1:10
            θ = (tj-1)*2*pi/10
            x,y,z = f(θ,ti)
            println(x," ",y," ",z)
        end

    end
end

generate_data()