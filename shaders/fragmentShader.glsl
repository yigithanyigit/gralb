#version 330

in vec4 fragColor;
in vec2 fragUV;

out vec4 outColor;

uniform sampler2D tex1;
uniform sampler2D tex2;
uniform float blendFactor = 0.0;

void main()
{

   vec4 tex1Val = texture(tex1, fragUV);
   vec4 tex2Val = texture(tex2, fragUV);

   vec4 final = mix(tex1Val, tex2Val, blendFactor);
   outColor = final;
   //outColor = tex2Val;
}