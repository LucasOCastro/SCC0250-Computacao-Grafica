#version 400

// Recebe do programa
uniform sampler2D tex;

// Recebe da vertex shader
in vec2 v_uv;

void main(){
    vec4 c = texture2D(tex, v_uv);
    if (c.a < 0.9)      // completely transparent
        discard; 
    gl_FragColor = c;
}