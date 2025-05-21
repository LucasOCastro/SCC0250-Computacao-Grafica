#version 450 core

// Recebe do programa
uniform sampler2D tex;

// Recebe da vertex shader
in vec2 v_uv;

// Output da fragment shader
out vec4 fragColor;

void main(){
    vec4 c = texture(tex, v_uv);
    if (c.a < 0.9)      // completely transparent
        discard; 
    fragColor = c;
}